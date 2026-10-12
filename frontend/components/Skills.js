import useInView from '../lib/useInView';

function SkillBar({ name, proficiency, inView, delay }) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1.5">
        <span className="text-ink">{name}</span>
        <span className="text-ink-faint">{proficiency}%</span>
      </div>
      <div className="skill-track">
        <div
          className="skill-fill"
          style={{
            width: inView ? `${proficiency}%` : '0%',
            transitionDelay: `${delay}ms`,
          }}
        />
      </div>
    </div>
  );
}

export default function Skills({ categories = [] }) {
  const [ref, inView] = useInView({ threshold: 0.2 });

  if (!categories.length) return null;

  return (
    <section id="skills" className="py-24 px-5">
      <div className="max-w-4xl mx-auto" ref={ref}>
        <h2 className="section-heading">Skills</h2>
        <div className="grid md:grid-cols-2 gap-6">
          {categories.map((cat) => (
            <div key={cat.id} className="glass rounded-2xl p-6">
              <h3 className="font-heading font-medium text-ink mb-5">{cat.name}</h3>
              <div className="space-y-4">
                {cat.skills.map((skill, i) => (
                  <SkillBar
                    key={skill.id}
                    name={skill.name}
                    proficiency={skill.proficiency}
                    inView={inView}
                    delay={i * 80}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
