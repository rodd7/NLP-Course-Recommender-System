import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

const nbInternationalBold = localFont({
	src: "../../public/fonts/NB-International-Pro-Bold.woff",
	variable: "--nb-international-bold",
	weight: "900",
});
const nbInternationalRegular = localFont({
	src: "../../public/fonts/NB-International-Pro-Regular.woff",
	variable: "--nb-international-regular",
	weight: "400",
});
const nbInternationalItalic = localFont({
	src: "../../public/fonts/NB-International-Pro-Italic.woff",
	variable: "--nb-international-italic",
	weight: "400",
});

export const metadata: Metadata = {
	title: "UTS Course Recommendation System",
	description: "CRS",
	icons: {
		icon: "/favicon.ico",
	},
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en">
			<head>
				<style>
					{`:root {
						--nb-international-bold: ${nbInternationalBold.variable};
						--nb-international-regular: ${nbInternationalRegular.variable};
						--nb-international-italic: ${nbInternationalItalic.variable};
					}`}
				</style>
			</head>
			<body
				className={`${nbInternationalRegular.variable} ${nbInternationalBold.variable} ${nbInternationalItalic.variable}`}
			>
				{children}
			</body>
		</html>
	);
}
