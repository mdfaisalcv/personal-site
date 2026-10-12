import '../styles/globals.css';
import { spaceGrotesk, inter } from '../lib/fonts';

export default function App({ Component, pageProps }) {
  return (
    <div className={`${spaceGrotesk.variable} ${inter.variable}`}>
      <div className="bg-field" aria-hidden="true">
        <span className="bg-blob bg-blob-a" />
        <span className="bg-blob bg-blob-b" />
      </div>
      <Component {...pageProps} />
    </div>
  );
}
