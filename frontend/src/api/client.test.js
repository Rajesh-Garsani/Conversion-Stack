import test from "node:test";
import assert from "node:assert/strict";
import { normalizeApiError } from "./client.js";

test("normalizes API validation errors", () => {
  assert.deepEqual(normalizeApiError({ response: { status: 400, data: { errors: { email: ["Invalid email."] } } } }), {
    message: { email: ["Invalid email."] },
    status: 400,
  });
});

test("normalizes timeout errors", () => {
  assert.deepEqual(normalizeApiError({ code: "ECONNABORTED" }), {
    message: "The request timed out.",
    status: 0,
  });
});
