GET_BOOKING_MESSAGES_QUERY = """
SELECT
    id,
    author,
    author_username,
    (author_username = :current_username) AS is_me,
    is_admin,
    message,
    created_at
FROM public.projects_booking_messages
WHERE booking_id = :booking_id
  AND is_deleted = FALSE
ORDER BY created_at ASC
"""

INSERT_BOOKING_MESSAGE_QUERY = """
INSERT INTO public.projects_booking_messages (
    booking_id,
    author,
    author_username,
    is_admin,
    message
)
VALUES (
    :booking_id,
    :author,
    :author_username,
    :is_admin,
    :message
)
RETURNING
    id,
    author,
    author_username,
    TRUE AS is_me,
    is_admin,
    message,
    created_at
"""