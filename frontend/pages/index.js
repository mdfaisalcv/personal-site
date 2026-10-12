import Head from 'next/head';
import { getProfile } from '../lib/api';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import About from '../components/About';
import Education from '../components/Education';
import Experience from '../components/Experience';
import Skills from '../components/Skills';
import Projects from '../components/Projects';
import Contact from '../components/Contact';
import Footer from '../components/Footer';
import Reveal from '../components/Reveal';

export default function Home({ profile }) {
  const name = profile?.full_name || 'Your Name';

  return (
    <>
      <Head>
        <title>{`${name} — ${profile?.title || 'Portfolio'}`}</title>
        <meta
          name="description"
          content={profile?.tagline || `${name}'s personal portfolio and CV`}
        />
      </Head>

      <Navbar name={name} />
      <main>
        <Hero profile={profile} />
        <Reveal><About profile={profile} /></Reveal>
        <Reveal><Education items={profile?.education || []} /></Reveal>
        <Reveal><Experience items={profile?.experience || []} /></Reveal>
        <Skills categories={profile?.skill_categories || []} />
        <Reveal><Projects items={profile?.projects || []} /></Reveal>
        <Reveal><Contact profile={profile} /></Reveal>
      </main>
      <Footer name={name} />
    </>
  );
}

// Server-side render on every request so edits made in Django admin
// show up immediately without rebuilding the frontend.
export async function getServerSideProps() {
  const profile = await getProfile();
  return { props: { profile } };
}
