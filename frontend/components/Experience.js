export default function Experience({ items = [] }) {
  if (!items.length) return null;

  return (
    <section id="experience" className="py-24 px-5">
      <div className="max-w-2xl mx-auto">
        <h2 className="section-heading">Experience</h2>
        <div className="timeline">
          {items.map((exp) => (
            <div key={exp.id} className="timeline-node">
              <div className="flex flex-wrap justify-between items-baseline gap-x-4 gap-y-1">
                <h3 className="font-heading font-medium text-ink">{exp.role}</h3>
                <span className="text-sm text-data whitespace-nowrap">
                  {exp.start_date} – {exp.end_date || 'Present'}
                </span>
              </div>
              <p className="text-ink-muted text-sm mt-1">
                {exp.company}
                {exp.location ? `, ${exp.location}` : ''}
              </p>
              {exp.description && (
                <p className="text-ink-muted text-sm mt-2 leading-relaxed whitespace-pre-line">
                  {exp.description}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
