import { uniqueUsername } from './utils'

describe('Create account', () => {
  it('registers a new user and lands on the simulations page', () => {
    const username = uniqueUsername()

    cy.visit('/')
    cy.contains('a', 'Sign up').click()

    cy.contains('label', 'Username').find('input').type(username)
    cy.contains('label', 'Email').find('input').type(`${username}@example.com`)
    cy.contains('label', 'Password').find('input').type('Password123')
    cy.contains('button', 'Create account').click()

    cy.location('pathname').should('eq', '/simulations')
    cy.get('.sa-top-bar').should('contain.text', 'Stock Analyzer')
    cy.window().its('localStorage.token').should('exist')
  })

  it('shows an error when the username is already taken', () => {
    const username = uniqueUsername()

    cy.request('POST', 'http://localhost:8000/core/auth/register/', {
      username,
      email: `${username}@example.com`,
      password: 'Password123',
    })

    cy.visit('/')
    cy.contains('a', 'Sign up').click()

    cy.contains('label', 'Username').find('input').type(username)
    cy.contains('label', 'Email').find('input').type(`${username}@example.com`)
    cy.contains('label', 'Password').find('input').type('Password123')
    cy.contains('button', 'Create account').click()

    cy.get('.error').should('be.visible')
    cy.location('pathname').should('eq', '/')
  })
})
