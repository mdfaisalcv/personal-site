export default function Footer({ name }) {
  const year = new Date().getFullYear();
  return (
    <footer className="py-8 px-5 text-center text-sm text-ink-faint border-t border-white/5">
      © {year} {name || 'Your Name'}. Built with Django &amp; Next.js.
    </footer>
  );
}
