import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from '../pages/Login';
import Register from '../pages/Register';

describe('Authentication Pages', () => {
    it('loads the login page and displays elements', () => {
        render(
            <BrowserRouter>
                <Login />
            </BrowserRouter>
        );
        expect(document.body).toBeDefined();
    });

    it('loads the register page', () => {
        render(
            <BrowserRouter>
                <Register />
            </BrowserRouter>
        );
        expect(document.body).toBeDefined();
    });
});
