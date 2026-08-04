# Surya Peri — Resume Website

A static, professional resume webpage ready for free hosting on GitHub Pages, Netlify, Vercel, or Cloudflare Pages.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Resume webpage |
| `styles.css` | Styling (responsive + print-friendly) |
| `resume.md` | Markdown source of resume content |

## Local preview

Open `index.html` in any browser, or serve locally:

```bash
# Python
python -m http.server 8080

# Node (npx)
npx serve .
```

Then visit `http://localhost:8080`.

## Deploy to GitHub Pages (free)

1. Create a new GitHub repository (e.g. `surya-resume`).
2. Push this folder:

   ```bash
   git add .
   git commit -m "Add professional resume website"
   git remote add origin https://github.com/YOUR_USERNAME/surya-resume.git
   git push -u origin main
   ```

3. In GitHub: **Settings → Pages → Source** → Deploy from branch `main`, folder `/ (root)`.
4. Your site will be live at `https://YOUR_USERNAME.github.io/surya-resume/`.

## Deploy to Netlify (free)

1. Sign up at [netlify.com](https://www.netlify.com).
2. Drag and drop this folder onto the Netlify dashboard, **or** connect your GitHub repo.
3. Build command: *(leave empty)* · Publish directory: `.`
4. Netlify assigns a free `*.netlify.app` URL; you can add a custom domain later.

## Deploy to Vercel (free)

```bash
npx vercel
```

Follow prompts. No build step required — static files deploy as-is.

## Deploy to Cloudflare Pages (free)

1. Push to GitHub, then connect the repo in Cloudflare Pages.
2. Build command: *(none)* · Output directory: `/`

## Custom domain

All platforms above support free HTTPS and custom domain mapping (e.g. `resume.yourdomain.com`).

## Print / PDF

Use the **Download / Print PDF** button on the page, or press `Ctrl+P` / `Cmd+P` and choose "Save as PDF".
