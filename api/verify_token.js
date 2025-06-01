import { OAuth2Client } from 'google-auth-library';

const client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { idToken } = req.body;

  if (!idToken) {
    return res.status(400).json({ error: 'Missing ID token' });
  }

  try {
    const ticket = await client.verifyIdToken({
      idToken,
      audience: process.env.GOOGLE_CLIENT_ID,
    });

    const payload = ticket.getPayload();

    // Verified user info here
    return res.status(200).json({ email: payload.email, name: payload.name });
  } catch (error) {
    return res.status(401).json({ error: 'Invalid ID token' });
  }
}
