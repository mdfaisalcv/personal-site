export default function Education({ items = [] }) {
  if (!items.length) return null;

  return (
    <section id="education" className="py-24 px-5">
      <div className="max-w-2xl mx-auto">
        <h2 className="section-heading">Education</h2>
        <div className="timeline">
          {items.map((edu) => (
            <div key={edu.id} className="timeline-node">
              <div className="flex flex-wrap justify-between items-baseline gap-x-4 gap-y-1">
                <h3 className="font-heading font-medium text-ink">{edu.degree}</h3>
                <span className="text-sm text-data whitespace-nowrap">
                  {edu.start_year} – {edu.end_year || 'Present'}
                </span>
              </div>
              <p className="text-ink-muted text-sm mt-1">
                {edu.institution}
                {edu.field_of_study ? `, ${edu.field_of_study}` : ''}
              </p>
              {edu.result && (
                <p className="text-ink-faint text-xs mt-1">{edu.result}</p>
              )}
              {edu.description && (
                <p className="text-ink-muted text-sm mt-2 leading-relaxed">
                  {edu.description}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
