//@ts-nocheck

import { neon } from '@neondatabase/serverless';
import { NextResponse } from 'next/server';

const sql = neon(process.env.DATABASE_URL);

export async function POST(request) {
  try {
    const body = await request.json();
    const { fullName, organization, email, phone, readinessScore, checkedItems, consent } = body;

    if (!fullName || !organization || !email || !consent) {
      return NextResponse.json(
        { error: 'Required fields or DPDP consent missing.' },
        { status: 400 }
      );
    }

    const referenceId = `NVX-${Math.floor(10000 + Math.random() * 90000)}`;

    await sql`
      INSERT INTO scoping_inquiries (
        reference_id, full_name, organization_name, work_email, 
        phone_number, readiness_score, checked_items, consent_given
      )
      VALUES (
        ${referenceId}, ${fullName}, ${organization}, ${email}, 
        ${phone}, ${readinessScore || 0}, ${JSON.stringify(checkedItems || [])}, ${consent}
      )
    `;

    return NextResponse.json({
      success: true,
      referenceId,
      message: 'Scoping call request logged with DPDP consent trail.'
    }, { status: 201 });

  } catch (error) {
    console.error('Database Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}