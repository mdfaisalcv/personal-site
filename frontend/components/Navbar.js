import { useState } from 'react';

const links = [
  { href: '#about', label: 'About' },
  { href: '#education', label: 'Education' },
  { href: '#experience', label: 'Experience' },
  { href: '#skills', label: 'Skills' },
  { href: '#projects', label: 'Projects' },
  { href: '#contact', label: 'Contact' },
];

export default function Navbar({ name }) {
  const [open, setOpen] = useState(false);
  const firstName = name ? name.split(' ')[0] : 'Portfolio';

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass">
      <nav className="max-w-6xl mx-auto flex items-center justify-between px-5 py-4">
        <a href="#hero" className="font-heading font-semibold text-lg text-ink">
          {firstName}
          <span className="text-data">.</span>
        </a>

        <button
          className="md:hidden text-2xl text-ink"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? '✕' : '☰'}
        </button>

        <ul className="hidden md:flex gap-8 text-sm text-ink-muted">
          {links.map((l) => (
            <li key={l.href}>
              <a href={l.href} className="hover:text-ink transition-colors">
                {l.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      {open && (
        <ul className="md:hidden flex flex-col gap-1 px-5 pb-4 text-sm text-ink-muted">
          {links.map((l) => (
            <li key={l.href}>
              <a
                href={l.href}
                className="block py-2"
                onClick={() => setOpen(false)}
              >
                {l.label}
              </a>
            </li>
          ))}
        </ul>
      )}
    </header>
  );
}
