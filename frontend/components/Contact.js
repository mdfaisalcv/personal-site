import { useState } from 'react';
import { sendContactMessage } from '../lib/api';

const initialForm = { name: '', email: '', subject: '', message: '' };
const inputClass =
  'w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2.5 text-ink placeholder:text-ink-faint focus:outline-none focus:border-signal/60 focus:ring-1 focus:ring-signal/40 transition-colors';

export default function Contact({ profile }) {
  const [form, setForm] = useState(initialForm);
  const [status, setStatus] = useState('idle');

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus('sending');
    try {
      await sendContactMessage(form);
      setStatus('sent');
      setForm(initialForm);
    } catch (err) {
      setStatus('error');
    }
  }

  const socialLinks = [
    { key: 'github_url', label: 'GitHub' },
    { key: 'linkedin_url', label: 'LinkedIn' },
    { key: 'facebook_url', label: 'Facebook' },
    { key: 'website_url', label: 'Website' },
  ].filter((s) => profile?.[s.key]);

  return (
    <section id="contact" className="py-24 px-5">
      <div className="max-w-xl mx-auto">
        <h2 className="section-heading text-center">Get in touch</h2>

        {socialLinks.length > 0 && (
          <div className="flex flex-wrap justify-center gap-6 mb-10 text-sm text-ink-muted">
            {socialLinks.map((s) => (
              <a
                key={s.key}
                href={profile[s.key]}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-data transition-colors"
              >
                {s.label}
              </a>
            ))}
          </div>
        )}

        <form onSubmit={handleSubmit} className="glass rounded-2xl p-6 space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <input
              type="text"
              name="name"
              placeholder="Your name"
              required
              value={form.name}
              onChange={handleChange}
              className={inputClass}
            />
            <input
              type="email"
              name="email"
              placeholder="Your email"
              required
              value={form.email}
              onChange={handleChange}
              className={inputClass}
            />
          </div>
          <input
            type="text"
            name="subject"
            placeholder="Subject"
            value={form.subject}
            onChange={handleChange}
            className={inputClass}
          />
          <textarea
            name="message"
            placeholder="Your message"
            required
            rows={5}
            value={form.message}
            onChange={handleChange}
            className={inputClass}
          />
          <button type="submit" disabled={status === 'sending'} className="btn-primary disabled:opacity-60">
            {status === 'sending' ? 'Sending…' : 'Send message'}
          </button>

          {status === 'sent' && (
            <p className="text-data text-sm">Thanks — your message has been sent.</p>
          )}
          {status === 'error' && (
            <p className="text-spark text-sm">
              Something went wrong. Make sure the backend server is running.
            </p>
          )}
        </form>
      </div>
    </section>
  );
}
