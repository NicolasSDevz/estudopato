# Patologia da Polpa — site de revisão

Site estático (HTML + CSS + JS puro, sem build step) para revisão de
"Doenças da Polpa e Periápice" — Patologia Bucal, UNESC.

## Rodar localmente

Basta abrir `index.html` no navegador, ou servir a pasta com qualquer
servidor estático:

```bash
npx serve .
# ou
python -m http.server 8080
```

## Deploy na Vercel

**Opção A — arrastar e soltar (mais rápido):**
1. Acesse https://vercel.com/new
2. Arraste esta pasta (`site/`) inteira para a área de upload.
3. Pronto — a Vercel detecta que é um site estático automaticamente.

**Opção B — CLI:**
```bash
npm i -g vercel
cd site
vercel        # deploy de preview
vercel --prod # publica em produção
```

**Opção C — Git (recomendado para manter atualizado):**
1. Suba esta pasta para um repositório no GitHub/GitLab/Bitbucket.
2. Em https://vercel.com/new, importe o repositório.
3. Framework preset: "Other" (site estático) — não precisa de build command.

Não há variáveis de ambiente nem dependências — é só HTML/CSS/JS + imagens.

## Estrutura

```
index.html   página única (hero + guia/apostila, flashcards, quiz, tabela comparativa)
styles.css   estilos (tema claro/escuro automático + toggle manual)
app.js       lógica da aplicação
data.js      dados das doenças e do quiz (gerado a partir do dataset em /scripts)
images/      fotos clínicas e radiografias reais, com licença livre (ver créditos)
Guia_Revisao_Doencas_Polpa_Periapice.pdf   apostila completa (baixável pelo site)
Planilha_Comparativa_Patologias.pdf        tabela comparativa detalhada (baixável pelo site)
```

## Créditos das imagens

As fotos/radiografias reais usadas têm licença Creative Commons (CC0, CC BY,
CC BY-SA) via Wikimedia Commons, com autor e fonte exibidos junto de cada
imagem no próprio site (rodapé do cartão). Onde não havia imagem real com
licença livre disponível, foi usado um esquema ilustrativo autoral no
padrão didático "raio-X anotado" (fundo escuro, estruturas em tons claros).

## Atualizando o conteúdo

O conteúdo (textos, categorias, questões do quiz) vive em
`scripts/pathdata.py` no projeto de origem. Depois de editar, rode:

```bash
python scripts/build_site.py
```

para regerar esta pasta `site/`.
