import React, { FC, useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'

import Button from '../../ui/Button'
import Input from '../../ui/Input'
import { Loader } from '../../ui/Loader'
import { globalGet, globalPost } from '../../api/globalFetch'
import { endPoints } from '../../api/endPoints'

import './style.scss'

type ChatMessage = {
    id: number
    author: string
    author_username: string
    is_me: boolean
    is_admin: boolean
    message: string
    created_at: string
}

type ChatModalProps = {
    bookingId: number
    onClose: () => void
}

const POLLING_INTERVAL_MS = 5000

const ChatModal: FC<ChatModalProps> = ({ bookingId, onClose }) => {
    const [messages, setMessages] = useState<ChatMessage[]>([])
    const [text, setText] = useState('')
    const [loading, setLoading] = useState(true)

    const messagesEndRef = useRef<HTMLDivElement | null>(null)
    const messagesContainerRef = useRef<HTMLDivElement | null>(null)
    const pollingRef = useRef<NodeJS.Timeout | null>(null)
    const lastMessageIdRef = useRef<number | null>(null)

    /** Проверяем, что пользователь сейчас внизу чата */
    const isAtBottom = (): boolean => {
        const el = messagesContainerRef.current
        if (!el) return true

        return el.scrollHeight - el.scrollTop - el.clientHeight < 50
    }

    /** Скроллим чат вниз */
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    /** Загрузка сообщений (initial + polling) */
    const loadMessages = (silent: boolean = false) => {
        globalGet(
            `${endPoints.bookingMessages}/${bookingId}`,
            (data: ChatMessage[]) => {
                if (!data) return

                const lastId = data.length ? data[data.length - 1].id : null

                // Если новых сообщений нет — ничего не делаем
                if (lastMessageIdRef.current === lastId) {
                    if (!silent) setLoading(false)
                    return
                }

                lastMessageIdRef.current = lastId

                const shouldScroll = isAtBottom()

                setMessages(data)

                if (shouldScroll) {
                    setTimeout(scrollToBottom, 50)
                }

                if (!silent) {
                    setLoading(false)
                }
            }
        )
    }

    /** initial load + polling */
    useEffect(() => {
        setLoading(true)
        loadMessages()

        pollingRef.current = setInterval(() => {
            loadMessages(true) // silent polling
        }, POLLING_INTERVAL_MS)

        return () => {
            if (pollingRef.current) {
                clearInterval(pollingRef.current)
            }
        }
    }, [bookingId])

    /** Отправка сообщения */
    const sendMessage = async () => {
        if (!text.trim()) return

        await globalPost(
            `${endPoints.bookingMessageCreate}/${bookingId}`,
            () => {
                setText('')
                loadMessages()
            },
            { message: text }
        )
    }

    return createPortal(
        <div className="modal" onClick={onClose}>
            <div className="content chat" onClick={(e) => e.stopPropagation()}>
                <header className="chat-header">
                    <h3>Диалог по бронированию #{bookingId}</h3>
                </header>

                {loading ? (
                    <Loader/>
                ) : (
                    <div className="chat-messages" ref={messagesContainerRef}>
                        {messages.map((msg) => (
                            <div
                                key={msg.id}
                                className={`chat-message ${msg.is_me ? 'me' : 'other'}`}
                            >
                                <div className="bubble">
                                    <div className="meta">
                                        <span className="author">{msg.author}</span>
                                        {msg.is_admin && (
                                            <span className="role">админ</span>
                                        )}
                                    </div>

                                    <div className="text">{msg.message}</div>

                                    <span className="time">
                                        {new Date(msg.created_at).toLocaleTimeString()}
                                    </span>
                                </div>
                            </div>
                        ))}
                        <div ref={messagesEndRef}/>
                    </div>
                )}

                <footer className="chat-footer">
                    <div className="chat-input-row">
                        <Input
                            placeholder="Введите сообщение..."
                            value={text}
                            setValue={(v) => setText(String(v))}
                            type="text"
                            className="chat-input"
                            onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
                                if (e.key === 'Enter' && text.trim()) {
                                    e.preventDefault()
                                    sendMessage()
                                }
                            }}
                        />

                        <Button
                            type="primary"
                            className="chat-send-btn"
                            onClick={sendMessage}
                            isActive={!!text.trim()}
                        >
                            Отправить
                        </Button>
                    </div>
                </footer>
            </div>
        </div>,
        document.getElementById('root') as HTMLElement
    )
}

export default ChatModal
