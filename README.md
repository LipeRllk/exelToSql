
# 🧾 Gerador de SQL a partir de Excel com Flask

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

Este projeto permite que o usuário envie arquivos Excel, visualize abas e colunas, e gere comandos SQL com base em um template fornecido. O sistema organiza os arquivos por sessão e realiza limpeza automática após um período de inatividade.

---

## 🚀 Funcionalidades

- Upload de arquivos `.xlsx`
- Visualização das abas da planilha
- Visualização das colunas de uma aba
- Geração de comandos SQL usando templates com variáveis
- Download do arquivo `.sql` gerado
- Limpeza automática de arquivos temporários (uploads e saídas) após 15 minutos de inatividade por sessão

---

## 🧠 Tecnologias utilizadas

- Python 3.x
- Flask
- pandas
- HTML/CSS (frontend básico)
- JavaScript (AJAX para comunicação dinâmica)

---

## 📁 Estrutura de pastas

```
/uploads                ← Arquivos Excel temporários
/generated              ← Arquivos SQL gerados para download
/templates/index.html   ← Interface principal
app.py                  ← Backend principal
README.md               ← Este arquivo
LICENSE                 ← Licença MIT
```

---

## ⚙️ Como executar localmente

1. Clone este repositório:
   ```bash
   git clone https://github.com/LipeRllk/exelToSql
   cd exelToSql
   ```

2. Instale as dependências:
   ```bash
   pip install flask pandas
   ```

3. Execute o servidor:
   ```bash
   python app.py
   ```

4. Acesse no navegador:
   ```
   http://localhost:5000
   ```

---

## 🧹 Sobre limpeza de arquivos

- Os arquivos de upload e SQL são salvos com um identificador único de sessão.
- Um mecanismo verifica a data de modificação e remove arquivos com mais de **15 minutos**.
- Isso garante segurança e limpeza automática sem interferir em sessões ativas.

---

## 📌 Observações

- O template de SQL deve utilizar **placeholders com nomes iguais às colunas**, por exemplo:
  ```sql
  INSERT INTO tabela (nome, idade) VALUES ('{Nome}', {Idade});
  ```
- Certifique-se de que os nomes de coluna no Excel correspondem exatamente às chaves no template.

---

## 🛡️ Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
