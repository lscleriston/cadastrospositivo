import sys
import os

# Adicionar o diretório pai ao sys.path para que o módulo 'app' possa ser encontrado
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
"""