
# 🌀 Diffusion Models for Generative Modeling on MNIST

This project implements **denoising diffusion probabilistic models (DDPMs)** from scratch, using a U-Net-based ScoreNet architecture trained to predict noise in a Gaussian diffusion process. It was developed as part of the final project for *CMSC 25025 / STAT 37601: Machine Learning and Large-Scale Data Analysis* at the University of Chicago.

---

## 🧠 Project Overview

Diffusion models generate data (e.g. images) by reversing a gradual noising process. This repository implements both:

- The **forward process**, which corrupts data with Gaussian noise over discrete time steps.
- The **reverse process**, modeled by a neural network that predicts the added noise at each step to recover the original data.

This implementation focuses on noise prediction (ε-parameterization), using a ScoreNet built on a U-Net backbone with Gaussian Fourier embeddings for time conditioning.

---

## 📂 Files

- `DDPM.ipynb` — Main notebook containing:
  - Model architecture
  - Diffusion schedule and forward process
  - Loss implementation (noise prediction loss)
  - Training loop
  - Sampling procedure
  - Sample visualizations and FID evaluation

---

## 🏗️ Model Architecture

The score model is a **time-dependent U-Net** (`ScoreNet`) that processes noisy inputs `x_t` and time steps `t`. Key components:
- **Gaussian Fourier embeddings** for time encoding
- **GroupNorm layers** for stable training
- **Downsampling** via strided convolutions
- **Upsampling** via transposed convolutions and skip connections

The model predicts `ε_θ(x_t, t)`, the noise added at timestep `t`.

---

## 🧪 Experiments

- Trained on MNIST using 60 epochs
- 200 diffusion steps (`T = 200`)
- Linear β schedule from 1e-4 to 0.1
- Batch size: 100
- Learning rate: 0.01 with scheduler
- FID score computed on 1000 samples

---

## 🖼️ Sample Outputs

Generated MNIST-like samples from pure Gaussian noise using the learned reverse process. Samples were evaluated with FID for quality.

---

## 📈 Results

| Metric    | Score     |
|-----------|-----------|
| FID       | *≈ 10–12* |
| Training loss | Monotonically decreasing over 60 epochs |
| Sampling quality | High visual fidelity on MNIST digits |

---

## ⚙️ Requirements

```bash
pip install torch torchvision numpy matplotlib scipy scikit-learn
```

---

## 🚀 Run Instructions

To train the model:
```bash
# Open and run all cells in final.ipynb
```

To sample from the trained model and compute FID:
- Run the sampling cells in `final.ipynb`
- Visualizations and score output included in the notebook

---

## 📚 References

- [Ho et al., 2020 – Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
- Course: *Machine Learning and Large Scale Data Analysis* — University of Chicago

---

## 🧑‍💻 Author

**Patrick Lin**  
Undergraduate Student, University of Chicago  
May 2025
