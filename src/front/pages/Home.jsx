import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Home = () => {
	const [isAuthenticated, setIsAuthenticated] = useState(false);
	const navigate = useNavigate();

	useEffect(() => {
		// Check if user has a token
		const token = sessionStorage.getItem('token');
		if (!token) {
			navigate('/login');
		} else {
			setIsAuthenticated(true);
		}
	}, [navigate]);

	const handleLogout = () => {
		// Remove token and redirect to login
		sessionStorage.removeItem('token');
		navigate('/login');
	};

	return (
		<div className="container mt-5">
			<div className="row justify-content-center">
				<div className="col-md-8 text-center">
					<div className="card shadow">
						<div className="card-header bg-success text-white">
							<h2 className="mb-0">Área Privada</h2>
						</div>
						<div className="card-body">
							<div className="mb-4">
								<img
									src={rigoImageUrl}
									alt="Rigo"
									className="img-fluid rounded-circle mb-3"
									style={{ maxWidth: "150px" }}
								/>
							</div>
							<h3>¡Bienvenido!</h3>
							<p className="lead">
								Has accedido correctamente a una página protegida.
								<br />
								Esta sección solo es accesible con un token válido.
							</p>
							<div className="alert alert-info">
								Tu sesión está activa y autenticada.
							</div>
							<button
								onClick={handleLogout}
								className="btn btn-danger btn-lg mt-3"
							>
								Cerrar Sesión
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};