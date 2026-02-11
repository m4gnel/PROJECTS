import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@blinkdotnew/sdk@2.3.5";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { transcript, field, experienceLevel, category } = await req.json();

    const blink = createClient({
      projectId: Deno.env.get("BLINK_PROJECT_ID") || "",
      secretKey: Deno.env.get("BLINK_SECRET_KEY") || "",
    });

    const prompt = `You are a world-class senior recruiter and interview coach. 
Analyze the following interview transcript for a ${field} position (${category} type, ${experienceLevel} level).

TRANSCRIPT:
${transcript}

Provide a deep, structured analysis including:
1. An overall score (0-100).
2. Scores for specific metrics: Communication, Technical Depth, STAR Structure, Confidence.
3. Key strengths (bullet points).
4. Areas for improvement (bullet points).
5. A summary coaching remark as "Alex", the senior recruiter.
6. For each question asked, provide specific feedback.

Return the result as a JSON object matching this schema:
{
  "overallScore": number,
  "metrics": [
    { "name": "Communication", "score": number, "description": "string" },
    { "name": "Technical Depth", "score": number, "description": "string" },
    { "name": "STAR Structure", "score": number, "description": "string" },
    { "name": "Confidence", "score": number, "description": "string" }
  ],
  "strengths": ["string"],
  "improvements": ["string"],
  "coachRemark": "string",
  "questions": [
    { "question": "string", "answer": "string", "feedback": "string", "score": number }
  ]
}`;

    const { object } = await blink.ai.generateObject({
      model: "google/gemini-3-flash",
      system: "You are a professional interview analyzer. Output only valid JSON.",
      prompt,
      schema: {
        type: "object",
        properties: {
          overallScore: { type: "number" },
          metrics: {
            type: "array",
            items: {
              type: "object",
              properties: {
                name: { type: "string" },
                score: { type: "number" },
                description: { type: "string" }
              },
              required: ["name", "score", "description"]
            }
          },
          strengths: { type: "array", items: { type: "string" } },
          improvements: { type: "array", items: { type: "string" } },
          coachRemark: { type: "string" },
          questions: {
            type: "array",
            items: {
              type: "object",
              properties: {
                question: { type: "string" },
                answer: { type: "string" },
                feedback: { type: "string" },
                score: { type: "number" }
              },
              required: ["question", "answer", "feedback", "score"]
            }
          }
        },
        required: ["overallScore", "metrics", "strengths", "improvements", "coachRemark", "questions"]
      }
    });

    return new Response(JSON.stringify(object), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
