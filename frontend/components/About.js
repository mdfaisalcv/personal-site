const IconMail = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <rect x="3" y="5" width="18" height="14" rx="2" />
    <path d="m4 7 8 6 8-6" />
  </svg>
);
const IconPhone = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d="M6.5 3h3l1.5 5-2.5 1.5a11 11 0 0 0 5.5 5.5L15.5 12l5 1.5v3a2 2 0 0 1-2 2C10.5 18.5 5.5 13.5 4.5 5.5a2 2 0 0 1 2-2.5Z" />
  </svg>
);
const IconPin = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d="M12 21s7-7.2 7-12a7 7 0 1 0-14 0c0 4.8 7 12 7 12Z" />
    <circle cx="12" cy="9" r="2.4" />
  </svg>
);

export default function About({ profile }) {
  return (
    <section id="about" className="py-24 px-5">
      <div className="max-w-2xl mx-auto text-center">
        <h2 className="section-heading">About</h2>
        <p className="text-ink-muted leading-relaxed text-[17px]">
          {profile?.bio || 'Bio not added yet.'}
        </p>

        <div className="flex flex-wrap justify-center gap-x-8 gap-y-3 mt-10 text-sm text-ink-muted">
          {profile?.email && (
            <span className="flex items-center gap-2">
              <IconMail /> {profile.email}
            </span>
          )}
          {profile?.phone && (
            <span className="flex items-center gap-2">
              <IconPhone /> {profile.phone}
            </span>
          )}
          {profile?.address && (
            <span className="flex items-center gap-2">
              <IconPin /> {profile.address}
            </span>
          )}
        </div>
      </div>
    </section>
  );
}
