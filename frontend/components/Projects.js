import { mediaUrl } from '../lib/api';

export default function Projects({ items = [] }) {
  if (!items.length) return null;

  return (
    <section id="projects" className="py-24 px-5">
      <div className="max-w-5xl mx-auto">
        <h2 className="section-heading">Projects</h2>
        <div className="grid md:grid-cols-2 gap-6">
          {items.map((proj) => {
            const img = mediaUrl(proj.image);
            return (
              <div
                key={proj.id}
                className="glass rounded-2xl overflow-hidden flex flex-col relative transition-all duration-300 hover:-translate-y-1 hover:border-signal/40"
                style={{ transitionProperty: 'transform, border-color, box-shadow' }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.boxShadow = '0 16px 40px -12px rgba(139, 92, 246, 0.35)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <span
                  className="absolute top-0 left-0 right-0 h-[2px]"
                  style={{ background: 'linear-gradient(90deg, #8B5CF6, #22D3EE)' }}
                  aria-hidden="true"
                />
                {img && (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={img} alt={proj.title} className="w-full h-44 object-cover" />
                )}
                <div className="p-6 flex flex-col flex-1">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <h3 className="font-heading font-medium text-ink">{proj.title}</h3>
                    {proj.featured && (
                      <span
                        className="mt-1.5 w-1.5 h-1.5 rounded-full bg-spark shrink-0"
                        title="Featured project"
                      />
                    )}
                  </div>
                  <p className="text-ink-muted text-sm mb-4 flex-1 leading-relaxed">
                    {proj.description}
                  </p>
                  <div className="flex flex-wrap gap-2 mb-5">
                    {(proj.tech_list || []).map((tech) => (
                      <span
                        key={tech}
                        className="text-xs text-data bg-data/10 px-2.5 py-1 rounded-full"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                  <div className="flex gap-5 text-sm">
                    {proj.live_url && (
                      <a
                        href={proj.live_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-ink hover:text-data transition-colors underline decoration-white/20 underline-offset-4"
                      >
                        Live demo
                      </a>
                    )}
                    {proj.repo_url && (
                      <a
                        href={proj.repo_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-ink-muted hover:text-ink transition-colors underline decoration-white/20 underline-offset-4"
                      >
                        Source code
                      </a>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
