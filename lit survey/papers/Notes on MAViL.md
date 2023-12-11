Paper [link](https://paperswithcode.com/paper/mavil-masked-audio-video-learners)
Authors: Po-Yao Huang, Vasu Sharma, Hu Xu, Chaitanya Ryali, Haoqi Fan, Yanghao Li, Shang-Wen Li, Gargi Ghosh, Jitendra Malik, Christoph Feichtenhofer
Facebook Research
Year: 2022
# Abstract
We present Masked Audio-Video Learners (MAViL) to learn audio-visual representations
with three complementary forms of self-supervision: (1) reconstructing
masked raw audio and video inputs, (2) intra-modal and inter-modal contrastive
learning with masking, and (3) self-training to predict aligned and contextualized
audio-video representations learned from the first two objectives. Empirically,
MAViL achieves state-of-the-art audio-video classification performance
on AudioSet (53.3 mAP) and VGGSound (67.1% accuracy), surpassing recent
self-supervised models and supervised models that utilize external labeled data.
Notably, pre-training with MAViL not only enhances performance in multimodal
classification and retrieval tasks, but it also improves the representations of each
modality in isolation, without relying on information from the other modality
during uni-modal fine-tuning or inference. The code and models will be available
at https://github.com/facebookresearch/MAViL.

# Notes
- SOTA in [AudioSet](https://paperswithcode.com/dataset/audioset)
![[Pasted image 20231121180251.png]]
- Combines the ideas of masked auto-encoders and contrastive learning.
- "For audio, following [27, 64], it transforms a 10-second audio under 16K sampling rate into 128 Mel-frequency bands with a 25ms Hanning window shifting every 10ms. The resulting spectrogram is of dimension 1024 × 128. MAViL then tokenizes it into non-overlapping 16 × 16 patches where both time and frequency have a kernel and stride of 16. The flattened audio tokens have a sequence length N of 512."
- "Following the design choices in MAE, MAViL employs 12-layer Transformers (ViT-B) with 12 attention heads as the encoders for each modality . The embedding dimension H is set to 768. The audio-video fusion encoder layer consists of a 2-layer Transformer (vanilla or MBT) on top of the uni-modal encoders. Similarly, the audio and video decoders utilize 8-layer Transformers with an embedding dimension of 512 and 16 attention heads. MAViL’s audio/video encoder and decoder have 86M and 27M parameters, respectively. The floating point operations (FLOPs) for the audio encoder are 48.6G, comparable to the audio encoders in Audio-MAE and CAV-MAE."
- ![[Pasted image 20231121181035.png]]
- It is #14 on AudioSet for Audio-only classification

# Code
Not available for now
# Conclusions
- Self-supervision methods like contrastive learning and masked auto encoding can help us since we have less data to begin with.
