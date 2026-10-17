/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/AgriSage',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
