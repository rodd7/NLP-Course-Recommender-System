import { Navbar } from "../components/navbar";
import { Searchbar } from "@/components/searchbar";
import Head from "next/head";

export default function Home() {
	return (
		<div>
			<Head>
				<link rel="icon" href="/favicon.ico" />
			</Head>

			<Navbar />
			<div className="flex flex-row">
				{/* Left section */}
				<div className="basis-1/5 flex items-center justify-center "></div>

				<div className="basis-3/5 flex flex-col justify-center">
					<b className="text-5xl h-[25vh] flex items-center justify-center text-navbar">
						UTS Handbook Recommendation System
					</b>
					<Searchbar />
				</div>

				<div className="basis-1/5 flex items-center justify-center"></div>
			</div>
		</div>
	);
}
