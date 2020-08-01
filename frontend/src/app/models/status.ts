export interface Status{
    name: string,
    description: string,
}

export const STATUS_STATE = {
    submitted: 1,
    reviewed: 2,
    change: 3,
    approved: 4,
    denied: 5,
    expired: 6
}