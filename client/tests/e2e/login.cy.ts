import { uniqueUsername } from './utils'

describe('Login', () => {
  it('logs in an existing user and lands on the simulations page', () => {
    const username = uniqueUsername()

    cy.request('POST', 'http://localhost:8000/core/auth/register/', {
      username,
      email: `${username}@example.com`,
      password: 'Password123',
    })

    cy.visit('/')
    cy.contains('label', 'Username').find('input').type(username)
    cy.contains('label', 'Password').find('input').type('Password123')
    cy.contains('button', 'Log in').click()

    cy.location('pathname').should('eq', '/simulations')
    cy.get('.sa-top-bar').should('contain.text', 'Stock Analyzer')
    cy.window().its('localStorage.token').should('exist')
  })

  it('shows an error for invalid credentials', () => {
    cy.visit('/')
    cy.contains('label', 'Username').find('input').type('nonexistent-user')
    cy.contains('label', 'Password').find('input').type('WrongPassword123')
    cy.contains('button', 'Log in').click()

    cy.get('.error').should('be.visible').and('contain.text', 'Invalid credentials')
  })
})
