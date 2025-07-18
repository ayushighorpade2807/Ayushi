# -*- coding: utf-8 -*-
"""Assignment(Face Recognization).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AAxoqUj6OpGxBjNZS_l5wCoArvUNfVWc
"""

# Install required dependencies
!pip uninstall captum -y -q  # Remove any existing captum to avoid conflicts
!pip install captum==0.7.0 -q  # Install specific version for GradCAM compatibility
!pip install optuna torchsummary plotly numpy pandas matplotlib seaborn scikit-learn -q
!pip install torch torchvision -q  # Ensure PyTorch and torchvision are installed

# Verify installations
import pkg_resources
required = ['captum', 'optuna', 'torchsummary', 'plotly', 'numpy', 'pandas', 'matplotlib', 'seaborn', 'scikit-learn', 'torch', 'torchvision']
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = [pkg for pkg in required if pkg not in installed]
if missing:
    print(f"Missing packages: {missing}")
else:
    print("All dependencies installed successfully!")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
from torchvision import models, transforms
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from PIL import Image

# Load dataset
data = pd.read_csv("train.csv")

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Plot class distribution
plt.figure(figsize=(8, 4))
sns.countplot(x='emotion', data=data)
plt.title("Emotion Class Distribution")
plt.xticks(ticks=range(7), labels=emotion_labels)
plt.grid(True, axis='y')
plt.show()

# Show one image from each emotion
def show_sample_images(df):
    fig, axes = plt.subplots(1, 7, figsize=(20, 4))
    for i in range(7):
        img_data = df[df['emotion'] == i].iloc[0]['pixels']
        img = np.array(img_data.split(), dtype='uint8').reshape(48, 48)
        axes[i].imshow(img, cmap='gray')
        axes[i].axis('off')
        axes[i].set_title(emotion_labels[i])
    plt.tight_layout()
    plt.show()

show_sample_images(data)

# Split into train, val, test
train_data, temp_data = train_test_split(data, test_size=0.2, stratify=data['emotion'], random_state=42)
val_data, test_data = train_test_split(temp_data, test_size=0.5, stratify=temp_data['emotion'], random_state=42)

class FER2013Dataset(Dataset):
    def __init__(self, df, transform=None):
        self.images = df['pixels'].tolist()
        self.labels = df['emotion'].tolist()
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img = np.array(self.images[idx].split(), dtype='uint8').reshape(48, 48)
        img = Image.fromarray(img)
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]

# Transforms
transform_train = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

train_dataset = FER2013Dataset(train_data, transform_train)
val_dataset = FER2013Dataset(val_data, transform_test)
test_dataset = FER2013Dataset(test_data, transform_test)

from torchvision import transforms

# Training data augmentation pipeline
transform_train = transforms.Compose([
    transforms.RandomHorizontalFlip(),         # Flip image left/right
    transforms.RandomRotation(10),             # Rotate by ±10 degrees
    transforms.RandomCrop(44),                 # Crop a 44x44 region
    transforms.Resize((48, 48)),               # Resize back to 48x48
    transforms.ToTensor(),                     # Convert image to tensor
    transforms.Normalize(mean=[0.5], std=[0.5])  # Normalize to [-1, 1]
])

# No augmentation for validation and testing
transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

# Dataset class (same as before)
class FER2013Dataset(Dataset):
    def __init__(self, df, transform=None):
        self.images = df['pixels'].tolist()
        self.labels = df['emotion'].tolist()
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img = np.array(self.images[idx].split(), dtype='uint8').reshape(48, 48)
        img = Image.fromarray(img)
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]

# Create datasets with augmentations applied
train_dataset = FER2013Dataset(train_data, transform_train)
val_dataset = FER2013Dataset(val_data, transform_test)
test_dataset = FER2013Dataset(test_data, transform_test)

import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torch
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Define emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# --- Step 1: Dataset Class ---
class FER2013Dataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.dataframe = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        row = self.dataframe.iloc[idx]
        image = np.fromstring(row['pixels'], sep=' ', dtype=np.uint8).reshape(48, 48)
        label = int(row['emotion'])
        if self.transform:
            image = self.transform(image)
        return image, label

# --- Step 2: Define Transforms ---
augmentation_transform_full = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(10),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.RandomResizedCrop(size=(48, 48), scale=(0.8, 1.2)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

augmentation_transform_light = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(5),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# --- Step 3: Load Dataset (Assume you already have train_data as a DataFrame) ---
# Example placeholder: train_data = pd.read_csv('/path/to/fer2013.csv')
# Must already be loaded outside this block
# train_data must contain columns: ['emotion', 'pixels', ...]

# --- Step 4: Create Datasets and Loaders ---
train_dataset_aug_full = FER2013Dataset(train_data, augmentation_transform_full)
train_dataset_aug_light = FER2013Dataset(train_data, augmentation_transform_light)

train_loader_aug_full = DataLoader(train_dataset_aug_full, batch_size=64, shuffle=True)
train_loader_aug_light = DataLoader(train_dataset_aug_light, batch_size=64, shuffle=True)

# --- Step 5: Visualization Function ---
def plot_augmented_images(dataset, title, num_samples=5):
    fig, axes = plt.subplots(1, num_samples, figsize=(15, 3))
    for i in range(num_samples):
        index = torch.randint(0, len(dataset), (1,)).item()
        img, label = dataset[index]
        img = img.squeeze().cpu().numpy()
        img = 0.5 * img + 0.5  # Unnormalize
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(f"{emotion_labels[label]}")
        axes[i].axis('off')
    fig.suptitle(title, fontsize=16)
    plt.show()

# --- Step 6: Show Augmented Images ---
plot_augmented_images(train_dataset_aug_full, "Full Augmentation (Flip, Rotation, Shift, Zoom)")
plot_augmented_images(train_dataset_aug_light, "Light Augmentation (Flip, Rotation)")

# Hyperparameters
num_epochs = 20
batch_size = 64
learning_rate = 0.001
patience = 3
lr_reduce_factor = 0.5

# Class weights
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_data['emotion']),
    y=train_data['emotion'].values
)

sample_weights = [class_weights[label] for label in train_data['emotion'].values]
sampler = WeightedRandomSampler(sample_weights, len(sample_weights), replacement=True)

train_loader = DataLoader(train_dataset, batch_size=batch_size, sampler=sampler)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet18(pretrained=True)
model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
model.fc = nn.Linear(model.fc.in_features, 7)
model = model.to(device)

class_weights_tensor = torch.tensor(class_weights, dtype=torch.float).to(device)
criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', patience=patience, factor=lr_reduce_factor)

def train(model, loader):
    model.train()
    total_loss, correct = 0, 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * images.size(0)
        correct += (outputs.argmax(1) == labels).sum().item()
    return total_loss / len(loader.dataset), correct / len(loader.dataset)

def evaluate(model, loader):
    model.eval()
    total_loss, correct = 0, 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(1) == labels).sum().item()
    return total_loss / len(loader.dataset), correct / len(loader.dataset)

# Train model
train_losses, val_losses = [], []
train_accs, val_accs = [], []
best_val_acc = 0

for epoch in range(num_epochs):
    train_loss, train_acc = train(model, train_loader)
    val_loss, val_acc = evaluate(model, val_loader)

    train_losses.append(train_loss)
    val_losses.append(val_loss)
    train_accs.append(train_acc)
    val_accs.append(val_acc)

    scheduler.step(val_acc)

    print(f"Epoch {epoch+1}: Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}")

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "best_model.pth")

# Load best model
model.load_state_dict(torch.load("best_model.pth"))
model.eval()

# Plotting loss and accuracy
epochs = range(1, len(train_losses)+1)

plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
plt.plot(epochs, train_losses, label='Train Loss')
plt.plot(epochs, val_losses, label='Val Loss')
plt.title("Loss Over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs, train_accs, label='Train Accuracy')
plt.plot(epochs, val_accs, label='Validation Accuracy')
plt.title("Accuracy Over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Visualize predictions
def show_predictions(model, dataset, num_images=8):
    model.eval()
    plt.figure(figsize=(16, 4))
    for i in range(num_images):
        image, label = dataset[i]
        with torch.no_grad():
            output = model(image.unsqueeze(0).to(device))
            pred = output.argmax(1).item()

        img_np = image.squeeze().numpy()
        plt.subplot(1, num_images, i + 1)
        plt.imshow(img_np, cmap='gray')
        plt.title(f"P: {emotion_labels[pred]}\nT: {emotion_labels[label]}")
        plt.axis('off')
    plt.tight_layout()
    plt.show()

show_predictions(model, test_dataset)

pip install grad-cam

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

import numpy as np
import matplotlib.pyplot as plt
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

def show_gradcam(dataset, model, target_layers, index=0):
    model.eval()

    # Get image and label
    image_tensor, label = dataset[index]
    input_tensor = image_tensor.unsqueeze(0).to(device)

    # Denormalize grayscale image
    image_np = image_tensor.squeeze().cpu().numpy()
    image_np = 0.5 * image_np + 0.5  # Undo normalization
    image_np = np.clip(image_np, 0, 1)

    # Convert to RGB
    image_rgb = np.stack([image_np] * 3, axis=-1)

    # Run Grad-CAM with context
    with GradCAM(model=model, target_layers=target_layers) as cam:
        targets = [ClassifierOutputTarget(label)]
        grayscale_cam = cam(input_tensor=input_tensor, targets=targets)[0]
        cam_image = show_cam_on_image(image_rgb, grayscale_cam, use_rgb=True)

    # Plot original and Grad-CAM image
    plt.figure(figsize=(6, 3))
    plt.subplot(1, 2, 1)
    plt.imshow(image_np, cmap='gray')
    plt.title(f"Original (Label: {label})")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cam_image)
    plt.title("Grad-CAM")
    plt.axis('off')
    plt.show()

# Example usage (assuming you already have test_dataset and model ready):
target_layers = [model.layer4[-1]]  # For ResNet18
show_gradcam(test_dataset, model, target_layers, index=5)

plt.savefig("gradcam_output.png")