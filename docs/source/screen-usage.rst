Screen API usage

The Screen API is available on the same client via ``screen_api_key``.

.. code-block:: python

   """Screen API usage example."""

   import sys

   from coderpad.client import CoderPad
   from coderpad.screen_types import ScreenInvitation

   client = CoderPad(
       api_key="your-interview-api-key",
       screen_api_key="your-screen-api-key",
   )
   campaigns = client.screen.campaigns.list()
   _ = sys.stdout.write(campaigns[0].name)
   invitation = ScreenInvitation(
       candidate_email="candidate@example.com",
       candidate_name="Ada Lovelace",
   )
   result = client.screen.campaigns.send_invitation(
       campaign_id=campaigns[0].id,
       invitation=invitation,
   )
   if result.test_url is not None:
       _ = sys.stdout.write(result.test_url)

Manual invitations
------------------

Omit candidate identity to create a test link that you can share yourself.
Pass ``send_invitation_email=False`` to explicitly disable email delivery.
A candidate name is optional for both manual and email invitations.
Explicit email delivery requires a candidate email address.
When delivery is omitted, the server sends email only if an address is provided.
Set ``allow_duplicate_invitations=False`` on ``ScreenInvitation`` to ask the server to reject repeated invitations.
Omission uses the server default, which allows duplicates.
Explicit ``True`` allows them.

Account introspection
---------------------

Use ``client.user.get()`` to inspect the Interview key owner.
Its fields are ``name``, ``allow_pad_creation``, and ``analytics_id``.
Use ``client.screen.me()`` to inspect the Screen key owner, including ``organization_id``, ``recruiter_id``, and teams.
Each call uses the key for its product.
The asynchronous client exposes the same methods.

Creating campaigns
------------------

Use ``screen.campaigns.create`` with a name and an ordered list of ``ScreenCampaignQuestion`` or ``ScreenRandomQuestionSet`` entries.
Question IDs and team IDs are UUID strings.
The response is ``ScreenCreatedCampaign``, containing the integer campaign ID.

``ScreenRandomQuestionConfiguration`` selects domain, skills, question type, duration, and experience level.
Its included and excluded question ID lists are mutually exclusive.

``ScreenCampaignSettings`` supports locales, timers, invitation expiration, access windows, follow-up questions, webcam recording, full screen, copy and paste restrictions, simplified reports, AI Assist, and coding agents.
``enabled_coding_agents`` is sent as a string.
An empty string disables agents.
Omitted settings inherit team defaults.
Explicit false values are retained.
The service reports account feature restrictions and incompatible settings.
Campaign creation is never automatically retried.

AI Assist conversations
-----------------------

``client.screen.tests.ai_assist_conversations(test_id=11, question_id=question_uuid)`` returns ordered ``ScreenAIConversation`` values and ordered ``ScreenAIMessage`` values for a PROJECT question.
The question ID accepts a UUID or a UUID string.
Conversations become available after completion or while awaiting manual review.
The normal API error contract applies to missing project questions (404) and unfinished sessions (409).

Message roles retain ``USER`` or ``ASSISTANT``.
ISO 8601 creation timestamps are preserved as returned strings.
``output_items`` retains structured JSON, including unknown nested fields, text chunks, reasoning, and tool-call metadata.
It is ``None`` when omitted and an empty list when explicitly empty.
No output is collapsed into plain text.
Both synchronous and asynchronous clients support this operation.

Candidate project archives
--------------------------

``client.screen.tests.project_archive(test_id=11, question_id=question_uuid)`` returns the project ``tar.gz`` bytes with the candidate's changes applied.
The question ID accepts a UUID or a UUID string.
Save or extract these bytes only when your application requests it.
The SDK does not interpret them as JSON or PDF, extract files, or retry requests.
HTTP errors use the public ``CoderPadError`` contract, and transport errors propagate as they do for PDF downloads.
For slow project generation, configure the client's ``timeout`` or supply a Screen transport with an appropriate timeout.
The asynchronous client provides the same operation and supports normal task cancellation.

Question insights
-----------------

``client.screen.questions.insights(question_id=question_uuid)`` returns a typed ``ScreenQuestionInsights`` response.
Use ``programming_language`` to request language-specific statistics.
The question identity accepts a UUID or a UUID string.
Usage includes view count, last view timestamp, average duration in seconds, timeout ratio, and average score ratio.
Frequent answers and test-case success retain labeled counts and ratios, while score distribution retains zero, partial, and full score buckets and total candidates.
Absent statistics remain ``None`` and explicitly empty lists remain empty.
API errors use the usual error contract, including 400 and 404 responses.
Both synchronous and asynchronous clients provide the same operation.
