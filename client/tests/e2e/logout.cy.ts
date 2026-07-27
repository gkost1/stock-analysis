import { uniqueUsername } from './utils'

describe('Logout', () => {
  it('logs the user out and returns to the login screen', () => {
    const username = uniqueUsername()

    cy.request('POST', 'http://localhost:8000/core/auth/register/', {
      username,
      email: `${username}@example.com`,
      password: 'Password123',
    }).then(({ body }) => {
      cy.visit('/', {
        onBeforeLoad(win) {
          win.localStorage.setItem('token', body.token)
        },
      })
    })

    cy.get('.sa-top-bar').should('be.visible')
    cy.get('.sa-top-bar__menu-button').click()
    cy.contains('.sa-dropdown-item', 'Log out').click()

    cy.contains('h1', 'Log in').should('be.visible')
    cy.window().its('localStorage.token').should('not.exist')
  })
})
