"use server";

import OpenAI from "openai";
import dotenv from "dotenv";

dotenv.config();

const client = new OpenAI({
	apiKey: process.env.OPENAI_API_KEY,
});

console.log(process.env.OPENAI_API_KEY);

export async function generateEmbedding(
	text: string,
): Promise<number[] | null> {
	try {
		const response = await client.embeddings.create({
			model: "text-embedding-3-large",
			input: text,
		});

		return response.data[0].embedding;
	} catch (error) {
		console.error("Error generating embedding:", error);
		return null; // Return null if an error occurs
	}
}

// def generate_embedding(text: str) -> list[float]:

//     response = client.embeddings.create(
//         model="text-embedding-3-large",
//         input=text
//     )
//     return response.data[0].embedding
