# ExMAG: Exact Learning of Maximally Ancestral Graphs

This repository provides the official implementation of **ExMAG**, a score-based branch-and-cut algorithm designed for the exact learning of **Maximally Ancestral Graphs (MAGs)**.  
MAGs are a class of mixed graphs that represent both directed (causal) and bidirected (confounding) relationships, making them particularly useful in causal inference, especially in the presence of latent confounders.

The algorithm and its theoretical foundations are detailed in the paper:

> **ExMAG: Learning of Maximally Ancestral Graphs**  
> Petr Ryšavý, Pavel Rytíř, Xiaoyu He, Georgios Korpas, Jakub Mareček  
> [arXiv:2503.08245](https://arxiv.org/abs/2503.08245)

---

## Installation

```bash
git clone https://github.com/petrrysavy/exmag.git
cd exmag
pip install -r requirements.txt
```

## Usage

The main implementation for running the ExMAG algorithm is located in the `dagsolvers` directory. Please, see `solve_exmag.py`
for the details. At `solve_exmag.py:294`, you can also find a `main` function that shows an example how to call ExMAG with
a toy data. Here's a basic example of how to use it:
```bash
python -m dagsolvers.solve_exmag
```

## Citing

If you use this codebase in your research, please cite the following paper:

```bibtex
@misc{rysavy2025exmag,
      title={ExMAG: Learning of Maximally Ancestral Graphs}, 
      author={Petr Ryšavý and Pavel Rytíř and Xiaoyu He and Georgios Korpas and Jakub Mareček},
      year={2025},
      eprint={2503.08245},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2503.08245}, 
}
```

## License

This project is licensed under the [Apache License 2.0](https://github.com/petrrysavy/exmag/blob/main/LICENSE).