import os
import torch
from torchvision.models import resnet18, ResNet18_Weights
from torchvision import transforms
from PIL import Image

# Use the new weights API to load the pre-trained model.
weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights)
model.eval()

# Retrieve normalization values from weights metadata, with fallbacks if keys do not exist.
mean = weights.meta.get("mean", [0.485, 0.456, 0.406])
std = weights.meta.get("std", [0.229, 0.224, 0.225])

# Define a transformation pipeline using these normalization values.
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=mean, std=std)
])

# Determine path for imagenet_classes.txt relative to this file.
current_dir = os.path.dirname(os.path.abspath(__file__))
imagenet_path = os.path.join(current_dir, 'imagenet_classes.txt')

if not os.path.exists(imagenet_path):
    raise FileNotFoundError(
        f"imagenet_classes.txt not found in {current_dir}. "
        "Please download it from https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt and place it here."
    )

with open(imagenet_path, 'r') as f:
    imagenet_classes = {idx: class_name for idx, class_name in enumerate(f.read().splitlines())}

def analyze_image(image_path):
    """
    Analyze an image and return the top predicted labels.
    """
    image = Image.open(image_path).convert("RGB")
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)
    
    with torch.no_grad():
        output = model(input_batch)
    
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    results = []
    for i in range(top5_prob.size(0)):
        results.append({
            "class": imagenet_classes.get(top5_catid[i].item(), "Unknown"),
            "probability": top5_prob[i].item()
        })
    return results
