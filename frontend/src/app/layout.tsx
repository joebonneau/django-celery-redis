export const metadata = {
  title: "Protein Alignment",
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
