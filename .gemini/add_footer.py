import os
import re
from pathlib import Path

# Diretório raiz do projeto
root_dir = r"c:\Users\roger\OneDrive\Apresentações\Estátistica"

# Contador de arquivos modificados
modified_count = 0
skipped_count = 0

# Função para adicionar footer.js
def add_footer_script(file_path):
    global modified_count, skipped_count
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se já tem footer.js
        if 'footer.js' in content:
            print(f"⏭️  Pulado (já tem footer.js): {file_path}")
            skipped_count += 1
            return
        
        # Determina o caminho correto baseado na localização do arquivo
        rel_path = os.path.relpath(file_path, root_dir)
        
        # Conta quantos níveis de diretório estão acima
        depth = rel_path.count(os.sep)
        
        # Define o caminho do script baseado na profundidade
        if depth == 0:
            # Arquivo na raiz (index.html, anomalia.html, etc)
            script_path = 'assets/js/footer.js'
        elif depth == 2:
            # Arquivo em pages/subdir/ (pages/anomalia/z-score.html)
            script_path = '../../assets/js/footer.js'
        else:
            # Outros casos
            script_path = '../' * depth + 'assets/js/footer.js'
        
        # Procura por </body> e adiciona o script antes
        if '</body>' in content:
            # Adiciona o script antes de </body>
            new_content = content.replace(
                '</body>',
                f'  <script src="{script_path}"></script>\n</body>'
            )
            
            # Salva o arquivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Modificado: {rel_path} (script: {script_path})")
            modified_count += 1
        else:
            print(f"⚠️  Sem tag </body>: {rel_path}")
            skipped_count += 1
            
    except Exception as e:
        print(f"❌ Erro em {file_path}: {e}")
        skipped_count += 1

# Percorre todos os arquivos HTML
print("🔍 Procurando arquivos HTML...\n")

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            add_footer_script(file_path)

print(f"\n{'='*60}")
print(f"📊 RESUMO:")
print(f"   ✅ Arquivos modificados: {modified_count}")
print(f"   ⏭️  Arquivos pulados: {skipped_count}")
print(f"   📁 Total processado: {modified_count + skipped_count}")
print(f"{'='*60}")
