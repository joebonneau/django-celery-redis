import "bootstrap/dist/css/bootstrap.min.css";

export const metadata = {
  title: "Genome Alignment",
  description: "Joe Bonneau take-home",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
