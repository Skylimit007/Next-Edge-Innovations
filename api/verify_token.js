const { OAuth2Client } = require('google-auth-library');

const client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { idToken } = req.body;
  console.log('Received idToken:', idToken);
  console.log('Using GOOGLE_CLIENT_ID:', process.env.GOOGLE_CLIENT_ID);

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

    return res.status(200).json({ email: payload.email, name: payload.name });
  } catch (error) {
    console.error('Token verification error:', error);
    return res.status(401).json({ error: error.message || 'Invalid ID token' });
  }
};
