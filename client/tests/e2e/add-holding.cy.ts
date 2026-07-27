import { uniqueUsername } from './utils'

describe('Add holding', () => {
  it('creates a holding through the modal and renders it in the holdings table', () => {
    const username = uniqueUsername()

    cy.request('POST', 'http://localhost:8000/core/auth/register/', {
      username,
      email: `${username}@example.com`,
      password: 'Password123',
    }).then(({ body: { token, user } }) => {
      cy.request('POST', 'http://localhost:8000/core/testing/seed/', {
        factory: 'StudyFactory',
        attrs: {
          created_by_id: user.id,
          title: 'E2E Study',
          start_date: '2024-01-01',
          end_date: '2024-06-01',
        },
      }).then(({ body: study }) => {
        cy.visit(`/simulations/${study.id}`, {
          onBeforeLoad(win) {
            win.localStorage.setItem('token', token)
          },
        })
      })
    })

    cy.contains('h3', 'Holdings').should('be.visible')
    cy.contains('button', '+ Holding').click()

    cy.contains('label', 'Ticker').find('input').type('AAPL')
    cy.contains('label', 'Shares').find('input').type('10')
    cy.contains('label', 'Cost per Share').find('input').type('150')
    cy.contains('label', 'Date Purchased').find('input').type('2024-02-01')
    cy.contains('button', 'Add Holding').click()

    cy.get('.sa-portfolio-listing-table').should('be.visible')
    cy.contains('.sa-portfolio-listing-table tbody tr', 'AAPL').within(() => {
      cy.get('td').eq(0).should('have.text', '1')
      cy.get('td').eq(1).should('have.text', 'AAPL')
      cy.get('td').eq(2).should('have.text', '10')
      cy.get('td').eq(3).should('have.text', '$150.00')
      cy.get('td').eq(4).should('have.text', '2024-02-01')
    })
  })
})
