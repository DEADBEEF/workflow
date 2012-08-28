package edu.workflow.server.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Collection;

import edu.workflow.ping.PingPong.Job;
import edu.workflow.ping.PingPong.JobStatus;
import edu.workflow.ping.PingPong.JobStatusEnum;
import edu.workflow.ping.PingPong.JobType;
import edu.workflow.ping.PingPong.Jobs;

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
			createJobTable();
		} catch (SQLException e) {
			throw e;
		}
	}

	private void createUserTable() throws SQLException {
		Statement statement = connect.createStatement();
		statement.execute("CREATE TABLE IF NOT EXISTS tbl_users(" +
						"username VARCHAR(30), PRIMARY KEY(username))" );
		statement.close();
	}

	public void createJobTable() throws SQLException {
		Statement statement = connect.createStatement();
		statement.execute("CREATE TABLE IF NOT EXISTS tbl_jobs(" +
						"ID VARCHAR(30) PRIMARY KEY, type VARCHAR(30)," +
				         "asignee VARCHAR(30)," +
						 "description TEXT, status VARCHAR(10) )");
		statement.close();
	}

	public void addUser(String username) throws SQLException {
		PreparedStatement statement = connect
				.prepareStatement("INSERT INTO tbl_users VALUES(?)");
		statement.setString(1, username);
		statement.executeUpdate();
		statement.close();
	}

	public boolean checkJobExists(String jobId) throws SQLException {
		PreparedStatement statement = connect.prepareStatement("SELECT ID FROM tbl_jobs " +"" +
				"WHERE ID=?");
		statement.setString(1, jobId);
		statement.execute();
		if (statement.getResultSet().next()) {
			statement.close();
			return true;
		} else {
			statement.close();
			return false;
		}
	}

    public Jobs getJobList() throws SQLException {
        Statement statement = connect.createStatement();
        ResultSet results = statement.executeQuery("SELECT ID, type, asignee, "+ 
        			"description, status FROM tbl_jobs;");
        Jobs.Builder jobsBuilder = Jobs.newBuilder();
        while (results.next()) {
        	String ID = results.getString("ID");
        	String asignee = results.getString("asignee");
        	JobType type = JobType.valueOf(results.getString("type"));
        	String description = results.getString("description");
        	JobStatusEnum status = JobStatusEnum.valueOf(results.getString("status"));
        	jobsBuilder.addJobs(Job.newBuilder().setName(ID)
        		.setAssignee(asignee)
        		.setType(type)
        		.setDescription(description)
        		.setStatus(status).build());
        }	
        return jobsBuilder.build();
    }

	public JobStatusEnum checkStatus(String jobId) throws SQLException {
		PreparedStatement statement =  connect.prepareStatement("SELECT status FROM tbl_jobs " +
											"WHERE ID=?;");
		statement.setString(1, jobId);
		ResultSet results = statement.executeQuery();
		if (results.next()){
			String status = results.getString("status");
			return JobStatusEnum.valueOf(status);
		} else {
			return JobStatusEnum.JOBNOTFOUND;
		}
	}

	public void addJob(String jobId, JobType type, String asignee) throws SQLException {
		PreparedStatement statement = connect.prepareStatement("INSERT INTO tbl_jobs " +
				"values(?,?,?,?,?)");
		statement.setString(1, jobId);
		statement.setString(2, type.name());
		statement.setString(3, asignee);
		statement.setString(4, "none");
		statement.setString(5, JobStatusEnum.NOTDONE.name());
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
