package edu.workflow.server.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Collection;

public class Database {
	private Connection connect = null;

	
	public Database(String host, String user, String password, String database)
			throws ClassNotFoundException, SQLException {
		Class.forName("com.mysql.jdbc.Driver");
		try {
			connect = DriverManager
					.getConnection("jdbc:mysql://"+ host+ "/" + database,
							user,password);
			createUserTable();
		} catch (SQLException e) {
			throw e;
		}
	}
	
	private void createUserTable() throws SQLException {
		Statement statement = connect.createStatement();
		statement.execute("CREATE TABLE IF NOT EXISTS tbl_users(" +
						"username VARCHAR(30), PRIMARY KEY(username) )" );
		statement.close();
	}
	
	public void addUser(String username) throws SQLException {
		PreparedStatement statement = connect
				.prepareStatement("INSERT INTO tbl_users VALUES(?)");
		statement.setString(1, username);
		statement.executeUpdate();
		statement.close();
	}
	
	public Collection<String> getUsers() throws SQLException {
		Statement statement =  connect.createStatement();
		ResultSet results =  statement
				.executeQuery("SELECT username from tbl_users");
		ArrayList<String> users =  new ArrayList<String>();
		while (results.next()) {
			users.add(results.getString("username"));
		}
		results.close();
		statement.close();
		return users;
	}
	
	public void close() throws SQLException {
		connect.close();
	}

}
