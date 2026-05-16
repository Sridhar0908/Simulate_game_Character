import os
import torch
import numpy as np
from datetime import datetime
from PIL import Image
import rembg  # Background removal
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
from diffusers import StableDiffusionPipeline

# Global pipelines
_shape_pipeline = None
_image_pipeline = None
_device = 'cuda' if torch.cuda.is_available() else 'cpu'

def get_image_pipeline():
    global _image_pipeline
    if _image_pipeline is None:
        print("⏳ Loading Stable Diffusion...")
        _image_pipeline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if _device == 'cuda' else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        _image_pipeline.to(_device)
        print("✅ Stable Diffusion loaded!")
    return _image_pipeline

def get_shape_pipeline():
    global _shape_pipeline
    if _shape_pipeline is None:
        print(f"⏳ Loading Hunyuan3D-2 on {_device.upper()}...")
        _shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
            'tencent/Hunyuan3D-2',
            subfolder='hunyuan3d-dit-v2-0',
            variant='fp16' if _device == 'cuda' else None
        )
        _shape_pipeline.to(_device)
        print(f"✅ Hunyuan3D-2 loaded!")
    return _shape_pipeline

def remove_background(image: Image.Image) -> Image.Image:
    """Remove background from image - ESSENTIAL for clean 3D models."""
    print("🖼️ Removing background...")
    # Convert to RGBA if needed
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Use rembg for background removal
    output = rembg.remove(image)
    
    # Create white background
    white_bg = Image.new('RGBA', output.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white_bg, output)
    
    return composite.convert('RGB')

def clean_mesh(mesh):
    """Remove artifacts, bounding boxes, and smooth mesh."""
    print("🔧 Cleaning mesh artifacts...")
    
    # Remove small disconnected components (noise/artifacts)
    components = mesh.split(only_watertight=False)
    if len(components) > 1:
        # Keep largest component (main object), remove small debris
        largest = max(components, key=lambda x: x.vertices.shape[0])
        mesh = largest
        print(f"   Removed {len(components)-1} small artifacts")
    
    # Remove duplicate vertices
    mesh.merge_vertices()
    
    # Fix normals for proper lighting
    mesh.fix_normals()
    
    return mesh

def generate_3d_model(prompt: str, high_quality: bool = True):
    """
    Generate high-quality 3D model from text prompt.
    
    Args:
        prompt: Text description
        high_quality: If True, uses best settings (slower but better)
    """
    os.makedirs("static/models", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt)[:30]
    filename = f"{safe_prompt}_{timestamp}.glb"
    output_path = os.path.join("static/models", filename)
    
    # ==========================================
    # STEP 1: Generate high-quality image from text
    # ==========================================
    print(f"🎨 Step 1: Generating image from: '{prompt}'")
    
    image_pipe = get_image_pipeline()
    
    # Enhanced prompt for better 3D results
    enhanced_prompt = f"{prompt}, 3D render, white background, centered object, studio lighting, high detail"
    
    image = image_pipe(
        prompt=enhanced_prompt,
        num_inference_steps=50 if high_quality else 30,
        guidance_scale=7.5,
        height=512,
        width=512
    ).images[0]
    
    # Remove background (CRITICAL for clean 3D)
    image = remove_background(image)
    
    temp_image_path = f"static/models/temp_{timestamp}.png"
    image.save(temp_image_path)
    print(f"✅ Clean image saved")
    
    # ==========================================
    # STEP 2: Generate 3D with HIGH QUALITY settings
    # ==========================================
    print(f"🔧 Step 2: Generating 3D model (quality={'high' if high_quality else 'fast'})...")
    
    shape_pipe = get_shape_pipeline()
    
    # HIGH QUALITY parameters (no bounding box artifacts)
    mesh = shape_pipe(
        image=temp_image_path,
        num_inference_steps=50 if high_quality else 30,  # More steps = better quality
        guidance_scale=5.5,  # Optimal for shape accuracy
        octree_resolution=384 if high_quality else 256,  # Higher = more detail, no boxy artifacts
        max_faces=5000,  # Limit faces for clean topology (not 50k!)
        seed=42  # Reproducible
    )[0]
    
    # ==========================================
    # STEP 3: Clean mesh (remove artifacts)
    # ==========================================
    mesh = clean_mesh(mesh)
    
    # Export high-quality GLB
    mesh.export(output_path)
    print(f"✅ High-quality 3D model saved: {filename}")
    print(f"   Vertices: {len(mesh.vertices)}, Faces: {len(mesh.faces)}")
    
    # Cleanup temp
    os.remove(temp_image_path)
    
    return filename, output_path


def generate_3d_model_simple(prompt: str):
    """Fast mode with decent quality."""
    return generate_3d_model(prompt, high_quality=False)