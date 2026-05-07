"use server";

import { MongoClient } from "mongodb";
import { generateEmbedding } from "@/app/api/createEmbedding";
import dotenv from "dotenv";

dotenv.config();

const uri = `mongodb+srv://crswebsrvhandle:${process.env.MONGODB_PASSWORD}@cluster0.d9bow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`;
const client = new MongoClient(uri);

export async function searchIndex(query: string): Promise<string | null> {
	try {
		await client.connect();
		const database = client.db("subject");
		const collection = database.collection("subjects");

		const queryVector = await generateEmbedding(query);

		const results = await collection
			.aggregate([
				{
					$vectorSearch: {
						queryVector: queryVector,
						path: "subjectEmbedding",
						numCandidates: 3000,
						limit: 20,
						index: "EmbeddingSemanticSearch",
					},
				},
				{
					$project: {
						subjectID: 1,
						subjectTitle: 1,
						subjectLink: 1,
						subjectAvailability: 1,
						subjectCreditPoints: 1,
						subjectOrganisationalName: 1,
						subjectLevel: 1,
						subjectResultType: 1,
						subjectDescription: 1,
						subjectSLO: 1,
						subjectCILO: 1,
						subjectStrategy: 1,
						subjectContent: 1,
						subjectAssessment: 1,
						descriptiveTags: 1,
						contextTags: 1,

						descriptionSnippet: { $substr: ["$subjectDescription", 0, 150] },
						score: { $meta: "vectorSearchScore" },
					},
				},
			])
			.toArray();

		const resultsList = results.map((doc) => ({
			"Subject ID": doc.subjectID,
			"Subject Title": doc.subjectTitle,
			"Vector Search Score": doc.score,
			subjectLink: doc.subjectLink,
			subjectAvailability: doc.subjectAvailability,
			subjectCreditPoints: doc.subjectCreditPoints,
			subjectOrganisationalName: doc.subjectOrganisationalName,
			subjectLevel: doc.subjectLevel,
			subjectResultType: doc.subjectResultType,
			subjectDescription: doc.subjectDescription,
			subjectSLO: doc.subjectSLO,
			subjectCILO: doc.subjectCILO,
			subjectStrategy: doc.subjectStrategy,
			subjectContent: doc.subjectContent,
			subjectAssessment: doc.subjectAssessment,
			descriptiveTags: doc.descriptiveTags,
			contextTags: doc.contextTags,
			Snippet: doc.descriptionSnippet,
		}));

		return JSON.stringify(resultsList, null, 4);
	} catch (error) {
		console.error("Error during vector search:", error);
		return null;
	} finally {
		await client.close();
	}
}
