import { OAuth2Client } from 'google-auth-library';

const client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { idToken } = req.body;

  console.log('Received token:', idToken);

  if (!idToken) {
    return res.status(400).json({ error: 'Missing ID token' });
  }

  try {
    const ticket = await client.verifyIdToken({
      idToken,
      audience: process.env.GOOGLE_CLIENT_ID,
    });

    const payload = ticket.getPayload();

    console.log('Token payload:', payload);

    // You can customize this to return what you want about the user
    return res.status(200).json({
      email: payload.email,
      name: payload.name,
      picture: payload.picture,
      // Any other info you want to send
    });
  } catch (error) {
    console.error('Token verification error:', error);
    return res.status(401).json({ error: 'Invalid ID token' });
  }
}
