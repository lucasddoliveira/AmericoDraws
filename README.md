# AmericoDraws

AmericoDraws é uma biblioteca Python para processar imagens e gerar trajetórias 3D para braços robóticos. A biblioteca transforma imagens em caminhos de desenho otimizados que podem ser executados por braços robóticos.


<p float="left">
  <img src="examples/1/input.png" alt="Input" width="30%" />
  <img src="examples/1/output/background_removed.png" alt="Background Removed" width="30%" />
  <img src="examples/1/output/contour.png" alt="Contour" width="30%" />
</p>

<p float="left">
  <img src="examples/1/output/3d_path.png" alt="Input" width="40%" />
  <img src="examples/1/output/final_result.png" alt="Top view sketch" width="40%" /> 
</p>

<p float="left">
  <img src="examples/2/input.png" alt="Input" width="30%" />
  <img src="examples/2/output/background_removed.png" alt="Background Removed" width="30%" />
  <img src="examples/2/output/contour.png" alt="Contour" width="30%" />
</p>

<p float="left">
  <img src="examples/2/output/3d_path.png" alt="Input" width="40%" />
  <img src="examples/2/output/final_result.png" alt="Top view sketch" width="40%" /> 
</p>

## Características Principais

- Remoção automática de fundo de imagens usando IA
- Extração de contornos e bordas de imagens
- Geração de trajetórias 3D otimizadas para braços robóticos
- Simplificação e otimização de caminhos para movimentos suaves
- Visualização 3D dos caminhos gerados
- Geração de comandos para controle de braços robóticos

## Instalação

```bash
pip install AmericoDraws
```

### Dependências

- rembg>=2.0.0
- numpy>=1.19.0
- matplotlib>=3.3.0
- opencv-python>=4.5.0
- Pillow>=8.0.0
- scikit-learn>=0.24.0
- networkx>=2.5.0

## Uso Rápido

```python
from AmericoDraws import independencia_ou_morte

# Processar uma imagem e gerar trajetória 3D
pontos = independencia_ou_morte(
    "caminho/para/imagem.png",
    "diretorio/saida",
    process_cell_size=1,
    points_cell_width=1,
    z_up=10,
    remove_background=True
)

print(f"Gerados {len(pontos)} pontos para trajetória do braço robótico")
```

## Função Principal

A função `independencia_ou_morte()` é o ponto de entrada principal da biblioteca:

```python
independencia_ou_morte(
    input_path,             # Caminho para a imagem de entrada
    output_dir="output",    # Diretório para salvar os resultados
    process_cell_size=1,    # Tamanho da célula para processamento
    points_cell_width=1,    # Largura da célula para geração de pontos
    upper_left_edge=None,   # Coordenadas do canto superior esquerdo [x, y, z, a, e, r]
    bottom_right_edge=None, # Coordenadas do canto inferior direito [x, y, z, a, e, r]
    z_up=10,                # Valor do eixo Z para movimento com caneta levantada
    remove_background=True, # Remover o fundo da imagem
    bg_threshold=10,        # Limiar para limpeza de bordas alfa
    bg_erode_pixels=1,      # Pixels para erosão do canal alfa
    threshold1=120,         # Primeiro limiar para detecção de bordas Canny
    threshold2=191,         # Segundo limiar para detecção de bordas Canny
    blur_size=3,            # Tamanho do kernel para blur Gaussiano
    distance_threshold=3,   # Limiar de distância para filtrar pontos
    epsilon=0.25,           # Valor epsilon para algoritmo Douglas-Peucker
    linewidth=1             # Grossura da linha do resultado final
)
```

## Fluxo de Processamento

1. **Remoção de Fundo**: Remove o fundo da imagem usando IA (opcional)
2. **Extração de Contornos**: Detecta bordas e contornos na imagem
3. **Conversão para Matriz**: Converte a imagem em uma matriz binária
4. **Geração de Pontos**: Cria uma matriz de pontos 3D otimizada
5. **Visualização**: Gera visualizações 3D e 2D dos caminhos
6. **Exportação**: Salva os comandos para o braço robótico

## Arquivos de Saída

A biblioteca gera vários arquivos de saída:

- `background_removed.png`: Imagem com fundo removido
- `contour.png`: Imagem com contornos extraídos
- `final_result.png`: Visualização 2D do desenho final
- `3d_path.png`: Visualização 3D do caminho do braço robótico
- `robot_commands.txt`: Comandos para o braço robótico (formato CSV)

## Exemplos Adicionais

### Personalização da Área de Desenho

```python
from AmericoDraws import independencia_ou_morte

# Definir área de desenho personalizada
upper_left = [0, 1000, 0, 0, 0, 0]   # [x, y, z, a, e, r]
bottom_right = [1000, 0, 0, 0, 0, 0] # [x, y, z, a, e, r]

pontos = independencia_ou_morte(
    "imagem.png",
    "saida",
    upper_left_edge=upper_left,
    bottom_right_edge=bottom_right,
    z_up=20
)
```

### Controle de Parâmetros de Detecção de Bordas

```python
pontos = independencia_ou_morte(
    "imagem.png",
    "saida",
    threshold1=100,    # Mais sensível à detecção de bordas
    threshold2=200,
    blur_size=5,       # Blur maior para reduzir ruído
    epsilon=0.5        # Simplificação de caminho mais agressiva
)
```

## Módulos

A biblioteca está organizada nos seguintes módulos:

- `contour_extraction.py`: Funções para extração de contornos
- `image_processor.py`: Processamento principal de imagens
- `path_planning.py`: Planejamento de trajetórias para o braço robótico
- `utils.py`: Funções utilitárias
- `visualization.py`: Ferramentas de visualização

## Contribuições

Contribuições são bem-vindas! Por favor, abra um issue ou pull request no repositório GitHub.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Autor

- Lucas Dantas - [lucasddoliveira@gmail.com](mailto:lucasddoliveira1@gmail.com)

## Repositório

[https://github.com/lucasddoliveira/AmericoDraws](https://github.com/lucasddoliveira/AmericoDraws)



# AmericoDraws

AmericoDraws is a Python library for processing images and generating 3D trajectories for robotic arms. The library transforms images into optimized drawing paths that can be executed by robotic arms.

<p float="left">
  <img src="examples/1/input.png" alt="Input" width="30%" />
  <img src="examples/1/output/background_removed.png" alt="Background Removed" width="30%" />
  <img src="examples/1/output/contour.png" alt="Contour" width="30%" />
</p>

<p float="left">
  <img src="examples/1/output/3d_path.png" alt="Input" width="40%" />
  <img src="examples/1/output/final_result.png" alt="Top view sketch" width="40%" /> 
</p>

<p float="left">
  <img src="examples/2/input.png" alt="Input" width="30%" />
  <img src="examples/2/output/background_removed.png" alt="Background Removed" width="30%" />
  <img src="examples/2/output/contour.png" alt="Contour" width="30%" />
</p>

<p float="left">
  <img src="examples/2/output/3d_path.png" alt="Input" width="40%" />
  <img src="examples/2/output/final_result.png" alt="Top view sketch" width="40%" /> 
</p>


## Key Features

- Automatic background removal using AI
- Contour and edge extraction from images
- Generation of optimized 3D trajectories for robotic arms
- Path simplification and optimization for smooth movement
- 3D visualization of generated paths
- Generation of commands for robotic arm control

## Installation

```bash
pip install AmericoDraws
```

### Dependencies

- rembg>=2.0.0
- numpy>=1.19.0
- matplotlib>=3.3.0
- opencv-python>=4.5.0
- Pillow>=8.0.0
- scikit-learn>=0.24.0
- networkx>=2.5.0

## Quick Start

```python
from AmericoDraws import independencia_ou_morte

# Process an image and generate a 3D trajectory
pontos = independencia_ou_morte(
    "caminho/para/imagem.png",
    "diretorio/saida",
    process_cell_size=1,
    points_cell_width=1,
    z_up=10,
    remove_background=True
)

print(f"Generated {len(points)} points for robotic arm trajectory")
```

## Main Function

The `independencia_ou_morte()` function is the main entry point of the library:

```python
independencia_ou_morte(
    input_path,             # Path to input image
    output_dir="output",    # Directory to save results
    process_cell_size=1,    # Cell size for processing
    points_cell_width=1,    # Cell width for point generation
    upper_left_edge=None,   # Coordinates of upper left corner [x, y, z, a, e, r]
    bottom_right_edge=None, # Coordinates of bottom right corner [x, y, z, a, e, r]
    z_up=10,                # Z-axis value for pen-up movement
    remove_background=True, # Remove background from image
    bg_threshold=10,        # Threshold for alpha edge cleanup
    bg_erode_pixels=1,      # Pixels to erode from alpha channel
    threshold1=120,         # First Canny edge detection threshold
    threshold2=191,         # Second Canny edge detection threshold
    blur_size=3,            # Kernel size for Gaussian blur
    distance_threshold=3,   # Distance threshold for point filtering
    epsilon=0.25,           # Epsilon value for Douglas-Peucker algorithm
    linewidth=1             # Line width of the final result
)
```

## Processing Pipeline

1. **Background Removal**: Removes image background using AI (optional)
2. **Contour Extraction**: Detects edges and contours in the image
3. **Matrix Conversion**: Converts image to binary matrix
4. **Point Generation**: Creates an optimized 3D point matrix
5. **Visualization**: Generates 3D and 2D path visualizations
6. **Export**: Saves commands for the robotic arm

## Output Files

The library generates several output files:

- `background_removed.png`: Image with background removed
- `contour.png`:  Image with extracted contours
- `final_result.png`: 2D visualization of final drawing
- `3d_path.png`: 3D visualization of robotic arm path
- `robot_commands.txt`: Commands for robotic arm (CSV format)

## Additional Examples

### Custom Drawing Area

```python
from AmericoDraws import independencia_ou_morte

# Define custom drawing area
upper_left = [0, 1000, 0, 0, 0, 0]   # [x, y, z, a, e, r]
bottom_right = [1000, 0, 0, 0, 0, 0] # [x, y, z, a, e, r]

points = independencia_ou_morte(
    "image.png",
    "output",
    upper_left_edge=upper_left,
    bottom_right_edge=bottom_right,
    z_up=20
)
```

### Edge Detection Parameter Control

```python
points = independencia_ou_morte(
    "image.png",
    "output",
    threshold1=100,    # More sensitive edge detection
    threshold2=200,
    blur_size=5,       # Larger blur to reduce noise
    epsilon=0.5        # More aggressive path simplification
)
```

## Modules

The library is organized into the following modules:

- `contour_extraction.py`: Functions for contour extraction
- `image_processor.py`: Main image processing
- `path_planning.py`: Trajectory planning for the robotic arm
- `utils.py`: Utility functions
- `visualization.py`: Visualization tools

## Contributions

Contributions are welcome! Please open an issue or pull request on the GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Lucas Dantas - [lucasddoliveira@gmail.com](mailto:lucasddoliveira1@gmail.com)

## Repository

[https://github.com/lucasddoliveira/AmericoDraws](https://github.com/lucasddoliveira/AmericoDraws)