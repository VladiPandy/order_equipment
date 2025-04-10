export const addSpacesBeforeCapitals = (str: string): string => {
    return str.replace(/([A-ZА-Я])/g, ' $1').trim()
} 