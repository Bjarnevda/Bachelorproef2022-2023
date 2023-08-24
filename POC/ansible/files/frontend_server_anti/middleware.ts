import { NextResponse } from "next/server";
import { NextRequest } from "next/server";
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const suspiciousUserAgents = require("./public/bad-user-agents.js");

const redis = new Redis({
  url: "https://tough-guinea-36001.upstash.io",
  token:
    "AYyhASQgMWNlOTRlYmQtN2EwYS00YjVhLTg5MmEtM2QwNTU3NGM0ODk3Zjg5ZjAzM2IyMDFmNDI1MGExNDE4ZjE4ZTQ4MTlkNjE=",
});

// Create a new ratelimiter, that allows 5 requests per 10 seconds
const ratelimit = new Ratelimit({
  redis: redis,
  limiter: Ratelimit.fixedWindow(5, "10 s"),
});

export async function middleware(request: NextRequest) {
  if (suspiciousUserAgents.includes(request.headers.get("user-agent"))) {
    return new Response("Acces forbidden", {
      status: 404,
    });
  }

  if (request.nextUrl.pathname.startsWith("/product")) {
    const identifier = "api";
    const result = await ratelimit.limit(identifier);

    if (result.success) {
      return NextResponse.next();
    } else {
      return new Response("Too many requests", {
        status: 429,
        headers: {
          "X-RateLimit-Limit": result.limit.toString(),
          "X-RateLimit-Remaining": result.remaining.toString(),
          "X-RateLimit-Reset": result.reset.toString(),
        },
      });
    }
  }
}
