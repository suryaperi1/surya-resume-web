# Surya Peri — Resume Website

A static, professional resume webpage ready for free hosting on GitHub Pages, Netlify, Vercel, or Cloudflare Pages.

## Files

| File | Purpose |
|------|---------|
| `resume.md` | **Source of truth** — edit this file |
| `generate.py` | Builds `index.html` from `resume.md` |
| `index.template.html` | HTML shell (layout, tabs, styling hooks) |
| `index.html` | Generated site (do not edit by hand) |
| `styles.css` | Styling (responsive + print-friendly) |
| `app.js` | Tab navigation |

## Update workflow

1. Edit **`resume.md`** only.
2. Regenerate the site:

   ```powershell
   cd C:\Users\surya\OneDrive\Automation\surya-resume-web
   python generate.py
   ```

   Or: `.\generate.ps1`

3. Commit and push **both** `resume.md` and `index.html`:

   ```powershell
   git add resume.md index.html
   git commit -m "Update resume content"
   git push origin main
   ```

### `resume.md` conventions

- Optional YAML at the top (`tagline`, `page_title`, `meta_description`).
- Contact line under your name: `**City, ST** · phone · email · [LinkedIn](url)`.
- Jobs: `### Company` then `**Role** · Start – End`, then bullet list.
- Wrap a bullet in `**double asterisks**` to highlight it on the site (DevSecOps bullets).
- Technical skills use a Markdown table (`Category` | `Technologies`).

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
