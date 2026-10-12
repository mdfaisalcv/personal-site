/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Produces a minimal, self-contained build (only the files needed to
  // run `node server.js`) — much smaller Docker image than a full node_modules copy.
  output: 'standalone',
  images: {
    remotePatterns: [
      { protocol: 'http', hostname: 'localhost' },
      { protocol: 'http', hostname: '127.0.0.1' },
      { protocol: 'http', hostname: 'backend' },
    ],
  },
};

module.exports = nextConfig;
