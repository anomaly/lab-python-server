""" Generic Stripe webhook handler

  Much of what Stripe does is asynchronous and requires a webhook to be
  configured to respond to events.

  Stripe assumes that if you send a 200 OK then the application was able 
  to process the message, if you send a 400 or otherwise then Stripe will
  keep retrying until it gets a 200 OK from the application.

  The design of the application should consider if the application is able
  to process i.e validate you have all the data you need and 200 OK.

  If for example the database is unavailable or you are unable to queue
  the message then return a 400 for Stripe to retry.

"""

from fastapi import APIRouter, Request,\
  Depends, HTTPException, Header, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

import stripe

from ...db import get_async_session
from ...config import config

 
"""Mounts all the sub routers for the authentication module"""
router = APIRouter(tags=["stripe"])

# Respond to Stripe's webhooks
# Note that include_in_schema=False and this will not appear
# in the OpenAPI documentation
@router.post("/webhook", include_in_schema=False)
async def stripe_webhook(
  request: Request,
  background_tasks: BackgroundTasks,
  STRIPE_SIGNATURE: str = Header(default=None),
  session: AsyncSession = Depends(get_async_session)
):
  """ Responds to Webhooks from Stripe

    Note that you will require to implement a Task for each handler, 
    these should generally live in the tasks package and you can

    STRIPE_WEBHOOK_SECRET is required to be set in the environment

    FastAPI will try and parse the request body for it to be useful
    in most use cases, however Stripe's library requires the raw
    request body for the decryption to work.

    Refer to request_body = await request.body() in FastAPI docs.

  """
  event = None

  request_body = await request.body()

  try:
    event = stripe.Webhook.construct_event(
      request_body,
      STRIPE_SIGNATURE,
      config.STRIPE_WEBHOOK_SECRET.get_secret_value()
    )
  except ValueError as e:
    # Invalid payload
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid payload"
    )
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid signature"
    )

  if event.type == 'invoice.payment_failed':
    payment_intent = event.data.object  # contains a stripe.PaymentIntent
    print('PaymentIntent was successful!')
  elif event.type == 'invoice.paid':
    payment_intent = event.data.object
  elif event.type == 'payment_method.attached':
    pass
  elif event.type == 'customer.subscription.created':
    pass
  elif event.type == 'customer.subscription.updated':
    subscription = event.data.object
    import logging
    logging.error(subscription)

  return { 
    "success": True 
  } 