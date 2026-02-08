export const endPoints: Record<string, string> = {
    auth: 'info/project',
    booking: 'info/bookings',
    filters: 'info/booking_lists',
    createFilters: 'booking/possible_create',
    feedback: 'booking/feedback',

    checkEditBooking: 'booking/possible_changes',
    editBooking: 'booking/change',
    deleteBooking: 'booking/cancel',

    newBooking: 'booking/create',

    infoEquipment: 'info/table_equipment',
    infoExecutor: 'info/table_executor',
    infoRatings: 'info/rating_executor',

    downloadBookings: 'info/download_bookings',
    downloadExecutors: 'info/download_executor',
    downloadEquipment: 'info/download_equipment',
    downloadRatings: 'info/download_ratings',

    bookingMessages: 'chat/booking/messages',
    bookingMessageCreate: 'chat/booking/messages',

}

