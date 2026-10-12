import { mediaUrl, cvDownloadUrl } from '../lib/api';
import NeuralField from './NeuralField';

export default function Hero({ profile }) {
  const photo = mediaUrl(profile?.photo);

  return (
    <section
      id="hero"
      className="relative min-h-screen flex items-center justify-center px-5 pt-24 pb-16 overflow-hidden"
    >
      <NeuralField />
      <div
        className="absolute inset-0"
        style={{
          background:
            'radial-gradient(ellipse 60% 50% at 50% 40%, rgba(5,7,13,0) 0%, #05070D 85%)',
        }}
        aria-hidden="true"
      />

      <div className="relative z-10 max-w-3xl mx-auto text-center">
        {photo && (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={photo}
            alt={profile.full_name}
            className="w-28 h-28 rounded-full object-cover mx-auto mb-6 border border-white/15 animate-rise-in"
            style={{ animationDelay: '0ms' }}
          />
        )}

        <p
          className="text-data text-sm tracking-wide mb-4 animate-rise-in"
          style={{ animationDelay: '60ms' }}
        >
          {profile?.title || 'Full Stack Web Developer'}
        </p>

        <h1
          className="font-heading text-4xl md:text-6xl font-semibold text-ink mb-5 animate-rise-in"
          style={{ animationDelay: '150ms' }}
        >
          {profile?.full_name || 'Your Name'}
        </h1>

        {profile?.tagline && (
          <p
            className="text-ink-muted text-lg max-w-xl mx-auto mb-9 animate-rise-in"
            style={{ animationDelay: '260ms' }}
          >
            {profile.tagline}
          </p>
        )}

        <div
          className="flex flex-wrap gap-4 justify-center animate-rise-in"
          style={{ animationDelay: '380ms' }}
        >
          <a href="#contact" className="btn-primary">
            Contact me
          </a>
          {profile && (
            <a href={cvDownloadUrl()} className="btn-ghost">
              Download CV
            </a>
          )}
        </div>
      </div>
    </section>
  );
}
